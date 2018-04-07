@echo off

conan export-pkg . intel-tbb/2018@tuncb/pangea -s arch="x86_64" --force || goto :error
conan test ./test_package intel-tbb/2018@tuncb/pangea -s arch="x86_64" -s build_type=Debug || goto :error
conan test ./test_package intel-tbb/2018@tuncb/pangea -s arch="x86_64" -s build_type=Release || goto :error

goto :success

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

:success
echo Success!
