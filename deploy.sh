#!/bin/bash
# 龙溪企服官网一键同步部署脚本
# 用法: ./deploy.sh
# 功能：同步本地longc-es-website/到GitHub Pages并部署到阿里云服务器

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="/root/longc-es-website"
SERVER="root@47.94.201.215"
SERVER_WEB_ROOT="/var/www/longc-es"

echo "🔍 1. 检查Git状态..."
cd "$REPO_DIR"
if [[ -n $(git status --porcelain) ]]; then
    echo "📦 有未提交的更改，提交中..."
    git add -A
    git commit -m "更新：$(date '+%Y-%m-%d %H:%M') 自动同步"
else
    echo "✅ 无新更改"
fi

echo "🚀 2. 推送到GitHub Pages..."
git push origin main

echo "🔁 3. 等待GitHub Pages部署...（15秒）"
sleep 15

echo "✅ 4. GitHub Pages 部署完成"
echo "📌 官网地址：https://www.longc-es.com"
