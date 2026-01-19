"""
Test script to validate the MEC filter functionality.
"""
from base_scraper import Lead


def test_mec_filter():
    """Test that MEC mentions are correctly identified."""
    print("Testing MEC filter...\n")
    
    # Test cases
    test_cases = [
        {
            'description': 'Curso online de tatuagem reconhecido pelo MEC',
            'should_detect': True
        },
        {
            'description': 'Aprenda tatuagem com os melhores profissionais',
            'should_detect': False
        },
        {
            'description': 'Formação autorizada MEC em estética',
            'should_detect': True
        },
        {
            'description': 'Curso profissional com certificado internacional',
            'should_detect': False
        },
        {
            'description': 'Instituição credenciada pelo Ministério da Educação',
            'should_detect': True
        },
        {
            'description': 'Melhor curso de tatuagem do Brasil',
            'should_detect': False
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        lead = Lead(
            name=f"Test Lead {i}",
            platform="Test",
            url="https://test.com",
            description=test_case['description']
        )
        
        has_mec = lead.check_mec_mentions()
        expected = test_case['should_detect']
        passed = has_mec == expected
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} Test {i}:")
        print(f"   Description: {test_case['description']}")
        print(f"   Expected MEC: {expected}, Got: {has_mec}\n")
        
        if not passed:
            all_passed = False
    
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed!")
    
    return all_passed


if __name__ == "__main__":
    test_mec_filter()
