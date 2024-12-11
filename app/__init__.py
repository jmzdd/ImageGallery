from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



# 创建Flask应用实例
app = Flask(__name__)

# 允许跨域访问
CORS(app)
#CORS(app, origins=["http://127.0.0.1:8080"])

# 配置文件
try:
    app.config.from_object('app.config.Config')
except ImportError:
    print('配置文件不存在，请修改config_demo.py为config.py以启用配置文件')
    exit()

db = SQLAlchemy(app)
# 导入路由和控制器
from app import routes
