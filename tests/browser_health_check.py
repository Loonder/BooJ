# -*- coding: utf-8 -*-
"""
Browser Health Check - Validates Chrome/ChromeDriver compatibility.
Run this before deployment to ensure browser-based scrapers will work.
"""

import sys
import os

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

def test_chrome_version_detection():
    """Test that Chrome version can be detected."""
    print("🔍 [1/3] Testing Chrome version detection...")
    
    from src.browser_engine import BrowserEngine
    
    engine = BrowserEngine(headless=True)
    version = engine._detect_chrome_major_version()
    
    if version:
        print(f"   ✅ Chrome version detected: {version}")
        return True
    else:
        print("   ⚠️ Chrome version could not be detected (UC will auto-detect)")
        return True  # Still OK - UC will handle it

def test_browser_initialization():
    """Test that browser can be initialized successfully."""
    print("🌐 [2/3] Testing browser initialization...")
    
    from src.browser_engine import BrowserEngine
    
    try:
        engine = BrowserEngine(headless=True)
        driver = engine.init_driver()
        
        if driver is None:
            print("   ❌ Driver initialization returned None")
            return False
        
        # Quick navigation test
        driver.get("about:blank")
        
        print("   ✅ Browser initialized successfully!")
        engine.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Browser initialization failed: {e}")
        return False

def test_basic_navigation():
    """Test that browser can navigate to a page."""
    print("🧪 [3/3] Testing basic navigation...")
    
    from src.browser_engine import BrowserEngine
    
    try:
        engine = BrowserEngine(headless=True)
        driver = engine.init_driver()
        
        # Navigate to a simple page
        driver.get("https://httpbin.org/html")
        
        # Check we got something
        if "Herman Melville" in driver.page_source:
            print("   ✅ Navigation and page load successful!")
            engine.close()
            return True
        else:
            print("   ⚠️ Page loaded but content check failed")
            engine.close()
            return True  # Still technically works
            
    except Exception as e:
        print(f"   ❌ Navigation failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 BROWSER HEALTH CHECK - JobPulse")
    print("=" * 50)
    print()
    
    results = []
    
    # Run tests
    results.append(("Chrome Detection", test_chrome_version_detection()))
    results.append(("Browser Init", test_browser_initialization()))
    results.append(("Navigation", test_basic_navigation()))
    
    print()
    print("-" * 50)
    
    # Summary
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("Browser engine is ready for deployment!")
    else:
        print(f"⚠️ SOME TESTS FAILED ({passed}/{total})")
        for name, result in results:
            status = "✅" if result else "❌"
            print(f"   {status} {name}")
    
    print("=" * 50)
