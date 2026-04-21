#!/usr/bin/env python3
"""完整的校对流程测试（模拟）"""

import sys
import os

# 设置工作目录
WORKSPACE = "/Users/yangtao/WorkBuddy/Claw/docProc"
sys.path.insert(0, os.path.join(WORKSPACE, "backend"))

from docx import Document
from app.services.document import DocumentParser
from app.services.segment import SegmentStrategy
from app.services.term_checker import TermConsistencyChecker
from app.services.style_analyzer import StyleAnalyzer

def test_full_workflow(file_path):
    """测试完整的文档处理流程"""
    print(f"\n{'='*60}")
    print(f"完整流程测试：{os.path.basename(file_path)}")
    print(f"{'='*60}")
    
    try:
        # 1. 提取文本
        print("\n[1/4] 提取文档内容...")
        text = DocumentParser.extract_text(file_path)
        print(f"      ✓ 提取成功：{len(text)} 字符")
        
        # 2. 智能分段
        print("\n[2/4] 智能分段...")
        segment_strategy = SegmentStrategy(max_length=500)
        segments = segment_strategy.segment(text)
        print(f"      ✓ 分割为 {len(segments)} 个段落")
        
        # 3. 术语一致性检查
        print("\n[3/4] 术语一致性检查...")
        term_checker = TermConsistencyChecker()
        term_issues = term_checker.check_and_suggest(text)
        print(f"      ✓ 发现 {len(term_issues)} 个术语不一致问题")
        if term_issues:
            print(f"      示例：{term_issues[0]['original']} -> {term_issues[0]['suggested']}")
        
        # 4. 风格分析
        print("\n[4/4] 风格一致性分析...")
        segment_texts = [seg[0] for seg in segments[:100]]  # 分析前 100 段
        style_issues = StyleAnalyzer.detect_style_inconsistencies(segment_texts)
        print(f"      ✓ 发现 {len(style_issues)} 个风格一致性问题")
        
        # 汇总
        print(f"\n{'='*60}")
        print(f"✓ 完整流程测试通过")
        print(f"  - 文档大小：{os.path.getsize(file_path) / 1024:.2f} KB")
        print(f"  - 文本长度：{len(text)} 字符")
        print(f"  - 原始段落：{len(DocumentParser.extract_paragraphs(file_path))}")
        print(f"  - 智能分段：{len(segments)}")
        print(f"  - 术语问题：{len(term_issues)}")
        print(f"  - 风格问题：{len(style_issues)}")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败：{str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "="*70)
    print("        智能文档校对系统 - 完整流程测试")
    print("="*70)
    
    test_dir = os.path.join(WORKSPACE, "test")
    test_files = [
        os.path.join(test_dir, 'test_file_1.docx'),
        os.path.join(test_dir, 'test_file_2.docx')
    ]
    
    results = []
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"\n⚠ 文件不存在：{file_path}")
            continue
        
        success = test_full_workflow(file_path)
        results.append({
            'file': os.path.basename(file_path),
            'success': success
        })
    
    # 汇总
    print("\n" + "="*70)
    print("  最终测试结果")
    print("="*70)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n测试文件：{total_count}")
    print(f"成功：{success_count}")
    print(f"失败：{total_count - success_count}")
    
    for result in results:
        status = "✓ 通过" if result['success'] else "✗ 失败"
        print(f"  {result['file']}: {status}")
    
    print("\n" + "="*70)
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！系统功能正常！\n")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
