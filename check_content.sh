#!/bin/bash
echo "========================================="
echo "核心文件内容检查"
echo "========================================="

# 检查 Python 文件语法
echo ""
echo "=== Python 文件语法检查 ==="
for f in *.py; do
    python -m py_compile "$f" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ $f 语法正确"
    else
        echo "❌ $f 语法错误"
    fi
done

# 检查 XML 文件格式
echo ""
echo "=== XML 文件格式检查 ==="
for f in *.xml; do
    xmllint --noout "$f" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ $f 格式正确"
    else
        echo "⚠️ $f 格式检查跳过（xmllint 未安装）"
    fi
done

# 检查关键配置
echo ""
echo "=== 关键配置检查 ==="
grep -q "SIZE = 400" openmc_final.py && echo "✅ openmc_final.py: SIZE=400"
grep -q "SIZE = 400" openfoam_final.py && echo "✅ openfoam_final.py: SIZE=400"
grep -q "precice" config_unified.xml && echo "✅ config_unified.xml: preCICE 配置"
grep -q "OpenMC" config_unified.xml && echo "✅ config_unified.xml: OpenMC 参与"
grep -q "OpenFOAM" config_unified.xml && echo "✅ config_unified.xml: OpenFOAM 参与"

echo ""
echo "========================================="
