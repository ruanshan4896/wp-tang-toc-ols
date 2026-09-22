#!/bin/bash
# Script hỗ trợ đóng gói thư mục công cụ thành file zip cho bản fork ruanshan4896/wp-tang-toc-ols

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "==> Đang đóng gói wptangtoc-ols.zip..."
rm -f wptangtoc-ols.zip
zip -q -r wptangtoc-ols.zip tool-wptangtoc-ols

echo "==> Đang đóng gói wptangtoc-ols-user.zip..."
rm -f wptangtoc-ols-user.zip
zip -q -r wptangtoc-ols-user.zip tool-wptangtoc-ols-user

echo "==> Kiểm tra tính toàn vẹn gói zip..."
unzip -t -q wptangtoc-ols.zip
unzip -t -q wptangtoc-ols-user.zip

echo "✔ Hoàn tất đóng gói! Sẵn sàng để git commit và git push."
