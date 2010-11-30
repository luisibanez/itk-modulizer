from vtk import *

treeFileName = "itkModules.xml"
graphFileName = "itkIncludes.csv"

reader1 = vtkXMLTreeReader()
reader1.SetFileName(treeFileName)
reader1.SetEdgePedigreeIdArrayName("tree edge")
reader1.GenerateVertexPedigreeIdsOff()
reader1.SetVertexPedigreeIdArrayName("id")

reader2 = vtkDelimitedTextReader()
reader2.SetFieldDelimiterCharacters(",")
reader2.SetFileName(graphFileName)

reader1.Update()
reader2.Update()

graph = vtkTableToGraph()
graph.AddInputConnection(reader2.GetOutputPort())
graph.AddLinkEdge("Field 0", "Field 1")

view = vtkHierarchicalGraphView()
view.SetInteractionModeTo3D()
view.DisplayHoverTextOff()
# view.SetShowTree(True)
view.SetLayoutStrategyToCone()
view.GetRenderWindow().SetMultiSamples(0)
view.SetHierarchyFromInputConnection(reader1.GetOutputPort())
view.SetGraphFromInputConnection(graph.GetOutputPort())
view.SetVertexColorArrayName("VertexDegree")
view.SetColorVertices(True)
view.SetVertexLabelArrayName("name")
view.SetVertexLabelVisibility(True)
view.SetScalingArrayName("TreeRadius")

view.Update()
view.SetGraphEdgeColorArrayName("graph edge")
view.SetColorGraphEdgesByArray(True)

# ct = vtkCosmicTreeLayoutStrategy()
# ct.SetNodeSizeArrayName("VertexDegree")
# ct.SetSizeLeafNodesOnly(True)
# view.SetLayoutStrategy(ct)

theme = vtkViewTheme.CreateMellowTheme()
theme.SetLineWidth(1)
view.ApplyViewTheme(theme)
theme.FastDelete()

view.ResetCamera()

view.GetInteractor().Initialize()
view.GetInteractor().Start()
