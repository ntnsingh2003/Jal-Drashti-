"""
Resource Allocation Optimizer
==============================
Optimally distribute rescue resources across affected areas
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from typing import List, Dict, Tuple
import json
import os

# Note: Dependency on geopandas and scipy.optimize.
# For demonstration purposes, we use simple data structures if GeoPandas is not available.

class ResourceAllocator:
    """
    Optimize distribution of rescue resources
    """
    
    def __init__(self, rescue_centers: List[Tuple[float, float]],
                 affected_clusters,
                 pathfinder):
        """
        Parameters:
        -----------
        rescue_centers : list of (lat, lon)
            Available resource staging locations
        affected_clusters : GeoDataFrame or list of dicts
            Population clusters requiring assistance
        pathfinder : RescuePathFinder
            For calculating travel times
        """
        self.centers = rescue_centers
        self.clusters = affected_clusters
        self.pathfinder = pathfinder
        
        # Calculate distance/time matrix
        self.cost_matrix = self._build_cost_matrix()
    
    def _build_cost_matrix(self):
        """
        Build cost matrix: cost[i,j] = time from center i to cluster j
        """
        n_centers = len(self.centers)
        n_clusters = len(self.clusters)
        
        cost_matrix = np.zeros((n_centers, n_clusters))
        
        for i, center in enumerate(self.centers):
            # Check if clusters is GeoDataFrame or list
            if hasattr(self.clusters, 'iterrows'):
                for j, cluster in self.clusters.iterrows():
                    target = (cluster.geometry.y, cluster.geometry.x)
                    result = self.pathfinder.find_path(center, target)
                    cost_matrix[i, j] = result['statistics']['time_min'] if "error" not in result else 9999
            else:
                for j, cluster in enumerate(self.clusters):
                    target = (cluster['lat'], cluster['lng'])
                    result = self.pathfinder.find_path(center, target)
                    cost_matrix[i, j] = result['statistics']['time_min'] if "error" not in result else 9999
        
        return cost_matrix
    
    def allocate_resources(self, n_resources: int, optimization_goal='min_max_time'):
        """
        Allocate resources to clusters
        """
        if optimization_goal == 'min_max_time':
            return self._allocate_min_max_time(n_resources)
        elif optimization_goal == 'min_avg_time':
            return self._allocate_min_avg_time(n_resources)
        else:
            return self._allocate_min_max_time(n_resources)
    
    def _allocate_min_max_time(self, n_resources):
        """
        Minimize maximum response time (fairness-based)
        """
        assignments = []
        n_clusters = len(self.clusters)
        cluster_assigned = np.full(n_clusters, False)
        cluster_response_times = np.full(n_clusters, np.inf)
        
        for _ in range(n_resources):
            worst_cluster = None
            worst_time = -1
            
            for j in range(n_clusters):
                if not cluster_assigned[j]:
                    best_time = np.min(self.cost_matrix[:, j])
                    if best_time > worst_time:
                        worst_time = best_time
                        worst_cluster = j
            
            if worst_cluster is None:
                break
            
            best_center = np.argmin(self.cost_matrix[:, worst_cluster])
            assignments.append((best_center, worst_cluster))
            cluster_assigned[worst_cluster] = True
            cluster_response_times[worst_cluster] = self.cost_matrix[best_center, worst_cluster]
        
        assigned_times = cluster_response_times[cluster_assigned]
        
        # Population calculation helper
        def get_total_pop(indices):
            if hasattr(self.clusters, 'iloc'):
                return int(self.clusters.iloc[indices]['population'].sum())
            return sum(self.clusters[i]['population'] for i in indices)

        assigned_indices = np.where(cluster_assigned)[0]

        return {
            'assignments': assignments,
            'max_response_time': float(np.max(assigned_times)) if len(assigned_times) > 0 else np.inf,
            'avg_response_time': float(np.mean(assigned_times)) if len(assigned_times) > 0 else np.inf,
            'clusters_covered': int(np.sum(cluster_assigned)),
            'coverage_population': get_total_pop(assigned_indices)
        }

    def _allocate_min_avg_time(self, n_resources):
        """
        Minimize average response time (efficiency-based)
        """
        n_clusters = len(self.clusters)
        if n_resources >= n_clusters:
            row_ind, col_ind = linear_sum_assignment(self.cost_matrix)
            assignments = list(zip(row_ind[:n_resources], col_ind[:n_resources]))
        else:
            # Subset based on population priority
            if hasattr(self.clusters, 'sort_values'):
                sorted_indices = self.clusters['population'].sort_values(ascending=False).index[:n_resources]
            else:
                sorted_indices = sorted(range(n_clusters), key=lambda i: self.clusters[i]['population'], reverse=True)[:n_resources]
            
            subset_cost = self.cost_matrix[:, sorted_indices]
            row_ind, col_ind = linear_sum_assignment(subset_cost)
            assignments = [(row_ind[i], sorted_indices[col_ind[i]]) for i in range(len(row_ind))]
        
        response_times = [self.cost_matrix[center, cluster] for center, cluster in assignments]
        covered_clusters = [cluster for _, cluster in assignments]
        
        def get_total_pop(indices):
            if hasattr(self.clusters, 'iloc'):
                return int(self.clusters.iloc[indices]['population'].sum())
            return sum(self.clusters[i]['population'] for i in indices)
            
        return {
            'assignments': assignments,
            'max_response_time': float(np.max(response_times)),
            'avg_response_time': float(np.mean(response_times)),
            'clusters_covered': len(assignments),
            'coverage_population': get_total_pop(covered_clusters)
        }

    def generate_deployment_plan(self, resources: Dict[str, int]):
        plan = {
            'resource_allocations': {},
            'deployment_sequence': [],
            'estimated_coverage': {},
            'recommendations': []
        }
        
        for resource_type, count in resources.items():
            if count == 0: continue
            plan['resource_allocations'][resource_type] = self.allocate_resources(count)
        
        # Sort clusters by population (List or GeoDataFrame)
        if hasattr(self.clusters, 'sort_values'):
            sorted_clusters = self.clusters.sort_values('population', ascending=False)
            cluster_list = [(idx, row) for idx, row in sorted_clusters.iterrows()]
        else:
            cluster_list = sorted(enumerate(self.clusters), key=lambda x: x[1]['population'], reverse=True)

        for i, (idx, cluster) in enumerate(cluster_list):
            population = cluster['population'] if isinstance(cluster, dict) else cluster.population
            cluster_id = cluster['cluster_id'] if isinstance(cluster, dict) else cluster.cluster_id
            
            cluster_plan = {
                'cluster_id': cluster_id,
                'population': population,
                'priority_rank': i + 1,
                'resources_needed': self._estimate_resources_needed(population)
            }
            plan['deployment_sequence'].append(cluster_plan)
        
        total_pop = sum(c['population'] if isinstance(c, dict) else c.population for c in (self.clusters if not hasattr(self.clusters, 'iterrows') else [r for _, r in self.clusters.iterrows()]))
        
        for resource_type, allocation in plan['resource_allocations'].items():
            coverage_pct = 100 * allocation['coverage_population'] / total_pop if total_pop > 0 else 0
            plan['estimated_coverage'][resource_type] = {
                'population': allocation['coverage_population'],
                'percentage': round(coverage_pct, 1),
                'clusters': allocation['clusters_covered']
            }
        
        plan['recommendations'] = self._generate_recommendations(plan, resources)
        return plan

    def _estimate_resources_needed(self, population):
        return {
            'ambulances': max(1, int(np.ceil(population / 100))),
            'boats': max(1, int(np.ceil(population / 200))),
            'relief_kits': int(np.ceil(population / 5))
        }

    def _generate_recommendations(self, plan, available_resources):
        recs = []
        for res, cov in plan['estimated_coverage'].items():
            if cov['percentage'] < 50:
                recs.append({'type': 'CRITICAL', 'message': f"Critical shortage of {res}. Only {cov['percentage']}% population covered."})
        return recs

    def export_geojson(self, allocation, output_path):
        features = []
        for center_idx, cluster_idx in allocation['assignments']:
            center = self.centers[center_idx]
            
            if hasattr(self.clusters, 'iloc'):
                cluster = self.clusters.iloc[cluster_idx]
                target_coords = [cluster.geometry.x, cluster.geometry.y]
                cluster_id = cluster.cluster_id
                pop = cluster.population
            else:
                cluster = self.clusters[cluster_idx]
                target_coords = [cluster['lng'], cluster['lat']]
                cluster_id = cluster['cluster_id']
                pop = cluster['population']

            features.append({
                'type': 'Feature',
                'geometry': {'type': 'LineString', 'coordinates': [[center[1], center[0]], target_coords]},
                'properties': {
                    'center_id': center_idx,
                    'cluster_id': cluster_id,
                    'population': pop,
                    'time_min': self.cost_matrix[center_idx, cluster_idx]
                }
            })
        
        with open(output_path, 'w') as f:
            json.dump({'type': 'FeatureCollection', 'features': features}, f)
