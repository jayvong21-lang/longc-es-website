# GitHub Actions配置说明

本文档介绍如何使用GitHub Actions自动化部署厦门龙溪传芳企业服务有限公司官网。

## GitHub Actions简介

GitHub Actions是GitHub提供的自动化工作流平台，可以用于：
- 自动部署网站到GitHub Pages
- 自动检查代码质量
- 自动运行测试
- 自动构建项目

## 配置GitHub Actions

### 1. 创建工作流文件

在项目根目录下创建 `.github/workflows/deploy.yml` 文件：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pages: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 2. GitHub Pages配置

#### 自动配置：
1. GitHub Actions会自动检测到 `deploy.yml` 文件
2. 当有代码推送到 `main` 分支时，会自动触发部署
3. 部署完成后，网站会自动更新

#### 手动触发：
1. 可以在GitHub Actions页面手动触发部署
2. 点击"Run workflow"按钮
3. 选择"main"分支

## 高级配置选项

### 1. 添加构建步骤

如果需要构建项目（如压缩文件），可以在工作流中添加构建步骤：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pages: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install

      - name: Build project
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 2. 添加代码检查

可以添加代码质量检查步骤：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Check HTML syntax
        run: |
          # 检查HTML语法
          echo "Checking HTML syntax..."
          # 可以添加HTML语法检查工具

      - name: Check CSS syntax
        run: |
          # 检查CSS语法
          echo "Checking CSS syntax..."
          # 可以添加CSS语法检查工具

  deploy:
    needs: quality-check
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pages: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

## 监控部署状态

### 1. GitHub Actions页面
- 进入GitHub仓库页面
- 点击"Actions"选项卡
- 查看工作流执行状态

### 2. 部署日志
- 每个工作流都有详细的执行日志
- 可以查看每一步的执行结果
- 如果失败，可以查看错误信息

### 3. GitHub Pages状态
- 进入仓库"Settings"页面
- 点击"Pages"选项卡
- 查看部署状态和访问统计

## 常见问题处理

### 1. 部署失败怎么办？
- **检查GitHub Actions配置**: 确保 `deploy.yml` 文件语法正确
- **检查权限设置**: 确保GitHub Pages权限已启用
- **检查分支名称**: 确保工作流配置的分支与实际分支匹配

### 2. 网站更新延迟怎么办？
- GitHub Pages部署通常需要几分钟
- 如果长时间未更新，可以手动触发工作流
- 检查GitHub Actions的执行状态

### 3. 如何回滚到旧版本？
- 在GitHub上查看提交历史
- 找到想要回滚的版本
- 重新推送该版本到GitHub
- GitHub Actions会自动部署旧版本

## 最佳实践

### 1. 分支策略
- **main分支**: 生产环境部署
- **develop分支**: 开发环境测试
- **feature分支**: 功能开发

### 2. 测试策略
- 在 `develop` 分支上测试新功能
- 通过GitHub Actions自动测试
- 确认无误后再合并到 `main` 分支

### 3. 部署频率
- 建议每次功能更新后部署
- 避免频繁的小更新
- 定期检查部署状态

### 4. 备份策略
- GitHub自动备份所有版本
- 建议保留本地备份
- 定期导出网站数据

## 扩展功能

### 1. 添加自动化测试
可以添加自动化测试工作流：

```yaml
name: Test and Deploy

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run tests
        run: |
          # 运行自动化测试
          echo "Running tests..."

  deploy:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pages: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 2. 添加性能监控
可以添加性能监控工作流：

```yaml
name: Performance Monitoring

on:
  schedule:
    - cron: '0 0 * * *'  # 每天凌晨执行

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run performance tests
        run: |
          # 运行性能测试
          echo "Running performance tests..."
```

## 技术支持

如需GitHub Actions配置技术支持，请联系：
- 邮箱：huang@longxi-group.com
- 钉钉：虾秘书应用