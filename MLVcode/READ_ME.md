## Verified Functions
- InitializeNeighborhoods.m
- rotateLinedrawing.m
- averageProperty.m - 2 sub else if statements need to be fixed
- lineIntersection.m - Gives results but no way to verify
- removeZeroLengthContours.m - Works, no way to check one if statement
- getDistanceFromLineSegment.m
- histogramToTable.m
- getMATpropertyStats.m
- allLDHistogramsToTable.m
- computeContourProperties.m - Checked on getcontourfeatures_Single.ipynb
- saveSceneLDsToTable.m - Tried on a small test case
- detectJunctions.m - No errors but need to check the results, lineIntersection is to be checked
- splitLDbyProperties.m
- splitLDbyHistogramWeights.m - The initial few lines of histogram needs to be checked
- applyCircularAperture.m 

## Coded Functions
- mapMATtoContour.m - Lots to be checked
- fitLineSegments.m - Needs a lot more to be checked   
- randomlyShiftContours.m - One line needs to be fixed

- segmentContoursAtJunctions.m     - Some lines need to be fixed
- generateFeatureDensityMap.m  - Complex
- predictContoursByStatsModel.m  - Check the table formation and model
- MATpropertiesToContours.m - Need to check the polylines
- drawContoursByStatsModel.m - Needs regression model
- mergeLineSegments.m - Check
- cleanupJunctions.m - Recursion needs to be checked

- splitLDbyStatsModel.m
- splitLDmiddleSegmentsVsJunctions.m

- computeAllMATproperties.m
- computeMATpropertyPerBranch.m
- computeAllMATfromVecLD.m
- computeMATproperty.m - Has trace dependencies

- traceSkeleton.m - GetConSeg function
- traceLinedrawingFromEdgeMap.m - setDiff, GetConSeg


# Yet to be written


## Trace Functions
- traceLineDrawingFromRGB.m


## Render Functions
- renderLinedrawing.m        
- renderLinedrawingProperty.m        
- renderMATproperty.m
- renderContoursByStatsModel.m
- renderJunctions.m

## Compute Functions
- computeJunctionAnglesTypes.m
- computeJunctions.m

## Import Functions
- importSVG.m

          