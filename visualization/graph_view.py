from vtk import *

csv_source = vtkDelimitedTextReader()
csv_source.SetFieldDelimiterCharacters("\t")
csv_source.SetHaveHeaders(True)
csv_source.SetDetectNumericColumns(True)
csv_source.SetFileName("Manifest.txt")

graph = vtkTableToGraph()
graph.AddInputConnection(csv_source.GetOutputPort())
# graph.AddLinkVertex("Filename", "Name", False)
graph.AddLinkVertex("Group", "Group", False)
graph.AddLinkVertex("Module", "Module", False)
# graph.AddLinkEdge("Filename", "Module")
graph.AddLinkEdge("Module", "Group")

view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(graph.GetOutputPort())
view.SetVertexLabelArrayName("label")
view.SetVertexLabelVisibility(True)
view.SetVertexColorArrayName("ids")
view.SetColorVertices(True)
view.SetLayoutStrategyToFast2D()

theme = vtkViewTheme.CreateMellowTheme()
theme.SetCellColor(.2,.2,.6)
theme.SetLineWidth(5)
theme.SetPointSize(10)
view.ApplyViewTheme(theme)
view.SetVertexLabelFontSize(20)
theme.FastDelete()

view.GetRenderWindow().SetSize(600, 600)
view.ResetCamera()
view.Render()
view.GetInteractor().Start()

