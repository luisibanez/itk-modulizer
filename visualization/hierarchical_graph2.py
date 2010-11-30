from vtk import *

treeFileName = "itkModulesNoGroups.xml"
graphFileName = "itkIncludes.csv"

reader1 = vtkXMLTreeReader()
reader1.SetFileName(treeFileName)
reader1.SetEdgePedigreeIdArrayName("tree edge")
reader1.GenerateVertexPedigreeIdsOff()
reader1.SetVertexPedigreeIdArrayName("id")

stringfilter = vtkStringToNumeric()
stringfilter.SetInputConnection(reader1.GetOutputPort())

reader2 = vtkDelimitedTextReader()
reader2.SetFieldDelimiterCharacters(",")
reader2.SetFileName(graphFileName)

reader1.Update()
reader2.Update()

graph = vtkTableToGraph()
graph.AddInputConnection(reader2.GetOutputPort())
graph.AddLinkEdge("Field 0", "Field 1")

view = vtkHierarchicalGraphView()
# view.SetInteractionModeTo3D()
view.DisplayHoverTextOff()
view.SetLayoutStrategyToTree()
view.GetRenderWindow().SetMultiSamples(0)
view.SetHierarchyFromInputConnection(stringfilter.GetOutputPort())
view.SetGraphFromInputConnection(graph.GetOutputPort())
# view.SetVertexColorArrayName("VertexDegree")
view.SetVertexColorArrayName("colorId")
view.SetColorVertices(True)
view.SetVertexLabelArrayName("name")
view.SetVertexLabelVisibility(True)
view.SetScalingArrayName("TreeRadius")

view.Update()
view.SetGraphEdgeColorArrayName("graph edge")
view.SetColorGraphEdgesByArray(True)
view.SetBundlingStrength(0.7)

ct = vtkTreeLayoutStrategy()
view.SetLayoutStrategy(ct)
ct.SetRadial(True)
ct.SetAngle(360)

theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(1)
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()

view.GetInteractor().Initialize()
view.GetInteractor().Start()
