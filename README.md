## 基本使用
- 系统使用 **Flask** 和 **Layui** 实现前后端一体的系统
- 测试账号：test，密码：test
- 系统集成无密码登录，即通过邮箱和邮箱验证码登录
- 无密码登录前需要现在 **config** 文件中配置邮件系统
- 系统分为管理员和普通员工两种角色
- 系统中管理员可更改是否需要无密码登录
- 本系统需要 **Redis** 的支持以获取验证码，启动系统前请确保你本地正在运行 **Redis** 服务
- 本系统使用的 **Layui** 版本是2.7.6

## 资料网站
- Flask [`https://flask.palletsprojects.com/`](https://flask.palletsprojects.com/)
- Flask中文网 [`https://flask.github.net.cn/`](https://flask.github.net.cn/)
- Layui [`https://layui.dev/`](https://layui.dev/)
- Layui英文版 [`https://github.com/MuZiCul/layui_us`](https://github.com/MuZiCul/layui_us)