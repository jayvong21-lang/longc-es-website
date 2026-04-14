# 部署指南

本文档详细介绍了厦门龙溪传芳企业服务有限公司官网的部署流程和配置方法。

## 部署选项

### 1. GitHub Pages部署（推荐）

GitHub Pages是最简单、免费的部署方式，适合静态网站。

#### 部署步骤：
1. **创建GitHub仓库**
   - 登录GitHub账号
   - 点击右上角"+"按钮，选择"New repository"
   - 填写仓库名称：`longxi-company-website`
   - 选择"Public"公开访问
   - 点击"Create repository"

2. **上传项目文件**
   - 进入新建的仓库页面
   - 点击"Upload files"按钮
   - 上传项目所有文件（index.html, style.css, README.md, images文件夹等）
   - 点击"Commit changes"

3. **启用GitHub Pages**
   - 进入仓库的"Settings"页面
   - 在左侧菜单中找到"Pages"选项
   - 在"Branch"部分选择"main"分支
   - 在"Source"中选择"/ (root)"根目录
   - 点击"Save"
   - 等待几分钟后，GitHub Pages会自动部署

4. **访问网站**
   - 部署成功后，可以在GitHub Pages设置页面看到网站地址
   - 默认地址：`https://<username>.github.io/longxi-company-website`
   - 或者：`https://longxi-company-website.github.io/`

### 2. 自定义域名部署

如果需要使用公司自有域名，可以配置自定义域名。

#### 配置步骤：
1. **购买域名**
   - 选择合适的域名服务商（阿里云、腾讯云等）
   - 购买域名：如 `longxi-group.com`

2. **DNS配置**
   - 在域名服务商的控制台配置DNS解析
   - 添加CNAME记录：
     - 主机记录：`www`
     - 记录类型：`CNAME`
     - 记录值：`<username>.github.io`
   - 或者添加A记录（IPv4）：
     - 主机记录：`@`
     - 记录类型：`A`
     - 记录值：`185.199.108.153`
     - 备用值：`185.199.109.153`, `185.199.110.153`, `185.199.111.153`

3. **GitHub Pages配置**
   - 在GitHub Pages设置页面添加自定义域名
   - 输入域名：`www.longxi-group.com`
   - 点击"Save"
   - GitHub会自动验证域名所有权

4. **HTTPS配置**
   - GitHub Pages会自动为自定义域名配置HTTPS
   - 等待几分钟后，HTTPS证书会自动部署

### 3. 本地部署

#### 开发环境配置：
1. **安装Node.js**
   ```bash
   # 下载Node.js安装包
   https://nodejs.org/
   ```

2. **安装Git**
   ```bash
   # 下载Git安装包
   https://git-scm.com/downloads
   ```

3. **克隆项目**
   ```bash
   git clone https://github.com/<username>/longxi-company-website.git
   ```

4. **预览网站**
   ```bash
   # 直接在浏览器打开index.html
   ```

### 4. Vercel部署（可选）

Vercel是另一个免费的静态网站托管平台，支持自动部署。

#### 部署步骤：
1. **注册Vercel账号**
   - 访问 https://vercel.com
   - 使用GitHub账号登录

2. **导入项目**
   - 点击"Import Project"
   - 选择GitHub仓库 `longxi-company-website`
   - 点击"Import"

3. **配置部署**
   - Vercel会自动识别项目类型
   - 点击"Deploy"
   - 等待部署完成

4. **访问网站**
   - Vercel会生成一个唯一的URL
   - 如：`https://longxi-company-website.vercel.app`

## 部署注意事项

### 图片优化
- 建议将图片压缩到合适大小
- 使用WebP格式可以获得更好的压缩效果
- 图片文件名应使用英文，避免中文路径问题

### SEO优化建议
- 在HTML文件中添加更多meta标签
- 添加网站描述、关键词等
- 考虑添加robots.txt文件

### 性能优化
- 压缩CSS和JavaScript文件
- 使用CDN加载Font Awesome图标库
- 考虑添加favicon图标

### 安全性
- GitHub Pages自动提供HTTPS
- 不需要配置SSL证书
- 定期更新依赖库版本

## 监控和维护

### 网站监控
- 定期检查网站访问速度
- 监控404错误页面
- 检查图片加载状态

### 内容更新
- 定期更新项目案例
- 替换为实际公司图片
- 更新联系方式信息

### 备份策略
- GitHub自动备份所有代码
- 建议定期导出网站数据
- 保留本地副本

## 常见问题

### 1. GitHub Pages部署失败怎么办？
- 检查文件名是否正确（index.html必须存在）
- 检查图片路径是否正确
- 确保没有使用中文文件名

### 2. 自定义域名无法访问怎么办？
- 检查DNS解析是否正确生效
- 等待DNS传播时间（通常需要几分钟到几小时）
- 检查GitHub Pages设置中的域名配置

### 3. 图片无法加载怎么办？
- 检查图片路径是否正确
- 确保图片文件大小不超过GitHub的限制
- 检查图片文件名是否包含特殊字符

### 4. 如何更新网站内容？
- 在本地修改文件后，重新上传到GitHub
- GitHub Pages会自动更新
- 或者使用Git命令行提交更新

## 技术支持

如需技术支持，请联系：
- 邮箱：huang@longxi-group.com
- 钉钉：虾秘书应用