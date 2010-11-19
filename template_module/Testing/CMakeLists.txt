include ("${@itk-module-name@_SOURCE_DIR}/Testing/MIDAS.cmake")

set(MIDAS_REST_URL "http://midas.kitware.com/api/rest")
set(MIDAS_KEY_DIR "${@itk-module-name@_SOURCE_DIR}/Testing/MIDAS_Keys")

add_executable(@ITK_MODULE_TEST_NAME@  @ITK_MODULE_TEST_NAME@.cxx)

target_link_libraries(@ITK_MODULE_TEST_NAME@  @itk-module-name@ )


#midas_add_test(ITK_MODULE_TEST_NAME "${EXECUTABLE_OUTPUT_PATH}/@ITK_MODULE_TEST_NAME@" MIDAS{INPUT_DATA.md5} OUPUT_DATA)
add_test(ITK_MODULE_TEST_NAME "${EXECUTABLE_OUTPUT_PATH}/@ITK_MODULE_TEST_NAME@" MIDAS{INPUT_DATA.md5} OUPUT_DATA)


