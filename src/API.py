from flask import Flask, request, send_file
import os
import subprocess
import zipfile
##这是我添加的注释
app = Flask(__name__)

@app.route('/api/upload_and_run', methods=['POST'])
def upload_and_run():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return 'No file part in the request.', 400

    file = request.files['file']

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，所以需要检查文件名是否为空
    if file.filename == '':
        return 'No selected file.', 400

    # 检查文件是否是.zip文件
    if not file.filename.endswith('.zip'):
        return 'File is not a .zip file.', 400

    # 将文件保存到指定的文件夹
    zip_path = os.path.join('/path/to/your/directory', file.filename)
    file.save(zip_path)

    # 解压缩文件到指定的文件夹
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('/path/to/your/directory')

    # 遍历解压后的文件，并将其保存到另一个指定的文件夹
    for filename in os.listdir('/path/to/your/directory'):
        if filename.endswith('.py'):
            os.rename(os.path.join('/path/to/your/directory', filename), os.path.join('/path/to/another/directory', filename))

    # 执行给定的Python文件列表
    python_files = ['/path/to/your/python/script1.py', '/path/to/your/python/script2.py', '/path/to/your/python/script3.py']
    for python_file in python_files:
        subprocess.call(['python', python_file])

    # 从指定的文件夹中读取文件，并将其作为响应返回
    return send_file('/path/to/your/output/file', as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)

##这是我添加的注释