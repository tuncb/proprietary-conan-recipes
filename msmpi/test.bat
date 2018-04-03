@echo off

conan export-pkg . msmpi/2008.2@tuncb/pangea -s arch="x86_64" --force || goto :error
conan test ./test_package msmpi/2008.2@tuncb/pangea -s arch="x86_64" || goto :error

conan export-pkg . msmpi/2008.2@tuncb/pangea -s arch="x86" --force || goto :error
conan test ./test_package msmpi/2008.2@tuncb/pangea -s arch="x86" || goto :error

goto :success

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

:success
echo Success!
