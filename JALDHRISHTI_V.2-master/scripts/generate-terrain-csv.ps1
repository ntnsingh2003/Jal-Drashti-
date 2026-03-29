param(
    [string]$OutputDir = "docs/generated"
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$configs = @(
    @{
        Id = "wayanad_meppadi"
        FileStem = "meppadi"
        Name = "Meppadi"
        District = "Wayanad"
        State = "Kerala"
        BaseElevation = 780.0
        BBox = @(76.10, 11.52, 76.17, 11.59)
        Formula = {
            param($x, $y, $baseElevation)
            $baseElevation + [Math]::Sin($x * 0.15) * 80 + [Math]::Cos($y * 0.12) * 60
        }
    },
    @{
        Id = "darbhanga"
        FileStem = "darbhanga"
        Name = "Darbhanga"
        District = "Darbhanga"
        State = "Bihar"
        BaseElevation = 53.0
        BBox = @(85.85, 26.12, 85.93, 26.19)
        Formula = {
            param($x, $y, $baseElevation)
            $baseElevation + [Math]::Sin($x * 0.1) * 2 + [Math]::Cos($y * 0.1) * 2
        }
    },
    @{
        Id = "dhemaji"
        FileStem = "dhemaji"
        Name = "Dhemaji"
        District = "Dhemaji"
        State = "Assam"
        BaseElevation = 53.0
        BBox = @(94.53, 27.45, 94.60, 27.51)
        Formula = {
            param($x, $y, $baseElevation)
            $baseElevation + [Math]::Sin(($x * 0.08) + ($y * 0.08)) * 5
        }
    }
)

$gridSize = 40

foreach ($config in $configs) {
    $minLon = $config.BBox[0]
    $minLat = $config.BBox[1]
    $maxLon = $config.BBox[2]
    $maxLat = $config.BBox[3]
    $stepLon = ($maxLon - $minLon) / $gridSize
    $stepLat = ($maxLat - $minLat) / $gridSize

    $rows = for ($x = 0; $x -lt $gridSize; $x++) {
        for ($y = 0; $y -lt $gridSize; $y++) {
            $lon = $minLon + ($x * $stepLon)
            $lat = $minLat + ($y * $stepLat)
            $elevation = & $config.Formula $x $y $config.BaseElevation

            [PSCustomObject]@{
                village_id = $config.Id
                village_name = $config.Name
                district = $config.District
                state = $config.State
                grid_x = $x
                grid_y = $y
                longitude = [Math]::Round($lon, 6)
                latitude = [Math]::Round($lat, 6)
                elevation_m = [Math]::Round($elevation, 2)
            }
        }
    }

    $csvName = "{0}_3d_terrain_points.csv" -f $config.FileStem
    $csvPath = Join-Path $OutputDir $csvName
    $rows | Export-Csv -NoTypeInformation -Encoding UTF8 $csvPath
    Write-Output ("Generated {0} with {1} rows" -f $csvPath, $rows.Count)
}
