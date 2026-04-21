from docx import Document
import sys
import os

# 添加后端路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.services.document import DocumentParser
from app.services.segment import SegmentStrategy

def test_document_parser(file_path):
    """测试文档解析功能"""
    print(f"\n{'='*50}")
    print(f"测试文档：{os.path.basename(file_path)}")
    print(f"{'='*50}")
    
    try:
        # 提取文本
        text = DocumentParser.extract_text(file_path)
        print(f"✓ 成功提取文本，长度：{len(text)} 字符")
        print(f"\n前 200 字符预览:\n{text[:200]}...\n")
        
        # 提取段落
        paragraphs = DocumentParser.extract_paragraphs(file_path)
        print(f"✓ 成功提取 {len(paragraphs)} 个段落")
        
        return text, paragraphs
    except Exception as e:
        print(f"✗ 解析失败：{str(e)}")
        return None, None

def test_segment_strategy(text):
    """测试智能分段功能"""
    print(f"\n{'='*50}")
    print("测试智能分段")
    print(f"{'='*50}")
    
    try:
        segment_strategy = SegmentStrategy(max_length=500)
        segments = segment_strategy.segment(text)
        
        print(f"✓ 成功分割为 {len(segments)} 个段落")
        print(f"\n分段详情:")
        for i, (seg_text, start, end) in enumerate(segments):
            print(f"  段落 {i+1}: {len(seg_text)} 字符 (位置 {start}-{end})")
            print(f"    预览：{seg_text[:100]}...")
        
        return segments
    except Exception as e:
        print(f"✗ 分段失败：{str(e)}")
        return None

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  智能文档校对系统 - 功能测试")
    print("="*60)
    
    test_dir = os.path.join(os.path.dirname(__file__), 'test')
    test_files = [
        os.path.join(test_dir, 'test_file_1.docx'),
        os.path.join(test_dir, 'test_file_2.docx')
    ]
    
    all_results = {}
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"\n⚠ 文件不存在：{file_path}")
            continue
        
        # 测试文档解析
        text, paragraphs = test_document_parser(file_path)
        
        if text:
            # 测试智能分段
            segments = test_segment_strategy(text)
            all_results[os.path.basename(file_path)] = {
                'text': text,
                'paragraphs': paragraphs,
                'segments': segments,
                'status': 'success'
            }
        else:
            all_results[os.path.basename(file_path)] = {
                'status': 'failed'
            }
    
    # 汇总结果
    print("\n" + "="*60)
    print("  测试结果汇总")
    print("="*60)
    
    success_count = sum(1 for r in all_results.values() if r.get('status') == 'success')
    total_count = len(all_results)
    
    print(f"\n测试文件：{total_count}")
    print(f"成功：{success_count}")
    print(f"失败：{total_count - success_count}")
    
    for filename, result in all_results.items():
        status = "✓ 通过" if result.get('status') == 'success' else "✗ 失败"
        print(f"\n  {filename}: {status}")
        if result.get('status') == 'success':
            print(f"    - 段落数：{len(result['paragraphs'])}")
            print(f"    - 分段数：{len(result['segments'])}")
            print(f"    - 文本长度：{len(result['text'])} 字符")
    
    print("\n" + "="*60)
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
