set(itk-module-name_SRC
LIST_OF_SOURCE_FILES
)


add_library(itk-module-name  ${itk-module-name_SRC})

target_link_libraries(itk-module-name  DEPENDENCY_LIBS)

#### install and export the target ####
file(GLOB headerFiles  "${itk-module-name_SOURCE_DIR}/Source/*.h")
file(GLOB templateFiles "${itk-module-name_SOURCE_DIR}/Source/*.txx")


install(FILES
  ${headerFiles}
  ${templateFiles}
  DESTINATION  include/itk-module-name-${version})


install(TARGETS itk-module-name
  EXPORT  ${itk-module-name-targets}
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib/itk-module-name-${version}
  )
export(TARGETS itk-module-name
  APPEND FILE ${itk-module-name-targets-build})
