# Creating a zipped contentShell binary:
1. Get the chromium source and follow the instructions to build.
2. `cd [chromium root]/src`
3. Clean build with just content_shell
```
rm -rf out/Release
gclient runhooks
ninja -C out/Release content_shell
```
4. Generate contentShell.zip
```
(cd out/Release; zip -9 -FS -r -x\*.a -x\*pyproto\* -x\*gen/\* -x\*obj/\* -x\*java_mojo\* -x\*Chromium.app\* -x\*.tmp -x\*DS_Store\* ../../contentShell.zip .)
```
5. Rename to the current rev.
```
cp contentShell.zip `git rev-parse HEAD`.mac.zip
```# Creating a zipped contentShell binary:
1. Get the chromium source and follow the instructions to build.
2. `cd [chromium root]/src`
3. Clean build with just content_shell
```
rm -rf out/Release
gclient runhooks
ninja -C out/Release content_shell
```
4. Generate contentShell.zip
```
(cd out/Release; zip -9 -FS -r -x\*.a -x\*pyproto\* -x\*gen/\* -x\*obj/\* -x\*java_mojo\* -x\*Chromium.app\* -x\*.tmp -x\*DS_Store\* ../../contentShell.zip .)
```
5. Rename to the current rev.
```
cp contentShell.zip `git rev-parse HEAD`.mac.zip
```