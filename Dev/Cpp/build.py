import sys
import os
import shutil
import subprocess
import multiprocessing

def replace_word(file_name, target_str, replace_str):
    text = ""
    with open(file_name, "r") as file:
        text = file.read()

    text = text.replace(target_str, replace_str)

    with open(file_name, "w") as file:
        file.write(text)

def import_generate_bindings():
    binding_generator = __import__("godot-cpp.binding_generator").binding_generator
    cwd = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(__file__), "godot-cpp"))
    binding_generator.generate_bindings("godot-headers/api.json", False)
    os.chdir(cwd)

import_generate_bindings()

os.chdir(os.path.dirname(__file__))

job_opt = " -j" + str(multiprocessing.cpu_count())

if "platform=windows" in sys.argv:
    replace_word("godot-cpp/Sconstruct", "/MD", "/MT")

    subprocess.run("scons platform=windows bits=32 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=windows bits=64 target=release" + job_opt, shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/windows", exist_ok = True)

    shutil.copy2("bin/libeffekseer.win32.dll", "../Godot/addons/effekseer/bin/windows/")
    shutil.copy2("bin/libeffekseer.win64.dll", "../Godot/addons/effekseer/bin/windows/")

elif "platform=osx" in sys.argv:
    subprocess.run("scons platform=osx bits=64 target=release" + job_opt, shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/osx", exist_ok = True)

    shutil.copy2("bin/libeffekseer.osx.dylib", "../Godot/addons/effekseer/bin/osx/")

elif "platform=android" in sys.argv:
    subprocess.run("scons platform=android android_arch=armv7 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=android android_arch=arm64v8 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=android android_arch=x86 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=android android_arch=x86_64 target=release" + job_opt, shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/android", exist_ok = True)

    shutil.copy2("bin/libeffekseer.android-armv7.so", "../Godot/addons/effekseer/bin/android/")
    shutil.copy2("bin/libeffekseer.android-arm64v8.so", "../Godot/addons/effekseer/bin/android/")
    shutil.copy2("bin/libeffekseer.android-x86.so", "../Godot/addons/effekseer/bin/android/")
    shutil.copy2("bin/libeffekseer.android-x86_64.so", "../Godot/addons/effekseer/bin/android/")

elif "platform=ios" in sys.argv:
    replace_word("godot-cpp/Sconstruct", "-version-min=10.0", "-version-min=9.0")

    subprocess.run("scons platform=ios ios_arch=armv7 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=ios ios_arch=arm64 target=release" + job_opt, shell = True)
    subprocess.run("scons platform=ios ios_arch=x86_64 target=release" + job_opt, shell = True)

    subprocess.run("lipo -create bin/libeffekseer.ios-armv7.dylib bin/libeffekseer.ios-arm64.dylib -output bin/libeffekseer.ios.dylib", shell = True)
    subprocess.run("lipo -create bin/libeffekseer.ios-x86_64.dylib -output bin/libeffekseer.ios-sim.dylib", shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/ios", exist_ok = True)
    
    shutil.copy2("bin/libeffekseer.ios.dylib", "../Godot/addons/effekseer/bin/ios/")
    shutil.copy2("bin/libeffekseer.ios-sim.dylib", "../Godot/addons/effekseer/bin/ios/")

elif "platform=linux" in sys.argv:
    subprocess.run("scons platform=linux bits=32 target=release use_llvm=1" + job_opt, shell = True)
    subprocess.run("scons platform=linux bits=64 target=release use_llvm=1" + job_opt, shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/linux", exist_ok = True)

    shutil.copy2("bin/libeffekseer.linux-32.so", "../Godot/addons/effekseer/bin/linux/")
    shutil.copy2("bin/libeffekseer.linux-64.so", "../Godot/addons/effekseer/bin/linux/")

elif "platform=html5" in sys.argv:
    subprocess.run("scons platform=html5 bits=32 target=release" + job_opt, shell = True)

    os.makedirs("../Godot/addons/effekseer/bin/html5", exist_ok = True)

    shutil.copy2("bin/libeffekseer.wasm32.wasm", "../Godot/addons/effekseer/bin/html5/")
