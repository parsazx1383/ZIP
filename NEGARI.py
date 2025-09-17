import marshal
import zlib
import base64
import py_compile
import os

# مرحله 1: کامپایل کد به بایت‌کد
# ابتدا فایل را به pyc کامپایل می‌کنیم
input_file = "GHABEL.py"
py_compile.compile(input_file, "temp.pyc")

# خواندن بایت‌کد از فایل pyc
with open("temp.pyc", "rb") as f:
    # رد کردن هدر فایل pyc (معمولاً 16 بایت در پایتون 3.8+)
    f.read(16)  # هدر را نادیده می‌گیریم
    code_obj = marshal.load(f)  # بایت‌کد را با marshal می‌خوانیم

# مرحله 2: سریال‌سازی بایت‌کد با marshal
bytecode = marshal.dumps(code_obj)

# مرحله 3: فشرده‌سازی با zlib
compressed = zlib.compress(bytecode)

# مرحله 4: کدگذاری به Base64
encoded = base64.b64encode(compressed).decode("utf-8")

# مرحله 5: تولید کد نهایی
final_code = f"""import marshal, zlib, base64
exec(zlib.decompress(base64.b64decode("{encoded}")))
"""

# ذخیره کد رمزگذاری‌شده در یک فایل
with open("encrypted_code.py", "w") as f:
    f.write(final_code)

# حذف فایل موقت
os.remove("temp.pyc")

print("کد رمزگذاری‌شده در 'encrypted_code.py' ذخیره شد.")
print("رشته Base64 رمزگذاری‌شده:")
print(encoded)