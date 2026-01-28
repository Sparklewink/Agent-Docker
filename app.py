import os
import subprocess
import threading
import platform
import logging
import time
import shutil
from flask import Flask, render_template_string

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [Core] %(message)s')

# 环境变量
NZ_SERVER = os.environ.get('NZ_SERVER', '你的面板IP:端口')
NZ_CLIENT_SECRET = os.environ.get('NZ_CLIENT_SECRET', '你的全局密钥')
NZ_TLS = os.environ.get('NZ_TLS', 'false')

# 定义持久化数据目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data') # 对应 /app/data

def run_background_service():
    time.sleep(5) # 等待 Flask 启动
    
    if not NZ_SERVER or not NZ_CLIENT_SECRET:
        logging.error("环境配置不全，跳过启动。")
        return

    # 确保数据目录存在
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    # 探针二进制文件的最终路径
    agent_executable = os.path.join(DATA_DIR, 'nezha-agent')

    # 只有当 binary 不存在时才下载，避免每次重启都下载
    if not os.path.exists(agent_executable):
        logging.info("检测到探针缺失，开始初始化...")
        try:
            arch_map = {'x86_64': 'amd64', 'aarch64': 'arm64'}
            machine_arch = platform.machine()
            nezha_arch = arch_map.get(machine_arch, 'amd64')
            
            download_url = f"https://github.com/nezhahq/agent/releases/latest/download/nezha-agent_linux_{nezha_arch}.zip"
            zip_path = os.path.join(DATA_DIR, "agent.zip")

            # 下载
            logging.info(f"下载组件: {download_url}")
            subprocess.run(['curl', '-L', '-f', download_url, '-o', zip_path], check=True)
            
            # 解压
            logging.info("解压组件...")
            subprocess.run(['unzip', '-o', zip_path, '-d', DATA_DIR], check=True)
            extracted_files = os.listdir(DATA_DIR)
            for f in extracted_files:
                if 'nezha-agent' in f and f != 'agent.zip' and f != 'config.yml':
                    full_path = os.path.join(DATA_DIR, f)
                    # 赋予执行权限
                    os.chmod(full_path, 0o755)
                    # 如果文件名不对，重命名为标准名
                    if f != 'nezha-agent':
                        shutil.move(full_path, agent_executable)
            
            if os.path.exists(zip_path):
                os.remove(zip_path)
                
            logging.info("组件安装完成。")
            
        except Exception as e:
            logging.error(f"组件安装失败: {e}")
            return

    logging.info("正在启动探针...")
    try:
        # 构造命令
        cmd = [agent_executable, '-s', NZ_SERVER, '-p', NZ_CLIENT_SECRET]
        if NZ_TLS.lower() == 'true':
            cmd.append('--tls')
        agent_process = subprocess.Popen(
            cmd, 
            cwd=DATA_DIR,  
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        logging.info(f"探针已启动，PID: {agent_process.pid}，工作目录: {DATA_DIR}")
        
    except Exception as e:
        logging.error(f"启动失败: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("<h1>System Monitor Online</h1>")

service_thread = threading.Thread(target=run_background_service)
service_thread.daemon = True
service_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
