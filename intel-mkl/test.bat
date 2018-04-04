@echo off

conan export-pkg . intel-mkl/2018@tuncb/pangea -s arch="x86_64" --force || goto :error
conan test ./test_package intel-mkl/2018@tuncb/pangea -s arch="x86_64" || goto :error
goto :success

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

:success
echo Success!
