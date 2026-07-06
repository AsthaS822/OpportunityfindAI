#!/usr/bin/env python
"""Final Comprehensive App Verification"""

import sys

def test_backend():
    """Test backend health and basic functionality"""
    import httpx
    
    print("\n" + "="*70)
    print("BACKEND VERIFICATION")
    print("="*70)
    
    # Test 1: Health check
    try:
        r = httpx.get("http://127.0.0.1:8000/health", timeout=5)
        if r.status_code == 200:
            print("✓ Backend Health: OPERATIONAL")
            health = r.json()
            print(f"  - Datasets: {health.get('datasets_loaded')} loaded")
            print(f"  - Records: {health.get('records_loaded')} total")
            print(f"  - Memory: {health.get('memory_usage')}")
            return True
        else:
            print(f"✗ Backend Health: FAILED ({r.status_code})")
            return False
    except Exception as e:
        print(f"✗ Backend Health: {str(e)}")
        return False

def test_frontend_build():
    """Check frontend build"""
    from pathlib import Path
    
    print("\n" + "="*70)
    print("FRONTEND VERIFICATION")
    print("="*70)
    
    dist_path = Path("dist/index.html")
    if dist_path.exists():
        print("✓ Frontend Build: COMPLETE")
        size = dist_path.stat().st_size
        print(f"  - Output: dist/ directory")
        print(f"  - index.html: {size} bytes")
        return True
    else:
        print("✗ Frontend Build: NOT FOUND")
        return False

def test_api_endpoint():
    """Test API discovery endpoint"""
    import httpx
    
    print("\n" + "="*70)
    print("API ENDPOINT VERIFICATION")
    print("="*70)
    
    try:
        r = httpx.post(
            "http://127.0.0.1:8000/discover",
            json={"query": "scholarships", "language": "en"},
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            print("✓ API /discover Endpoint: WORKING")
            print(f"  - Status: Success")
            print(f"  - Response fields: {len(data)} keys")
            print(f"  - Thinking steps: {len(data.get('thinking_steps', []))} steps")
            print(f"  - Opportunities found: {len(data.get('opportunities', []))}")
            return True
        else:
            print(f"✗ API /discover Endpoint: FAILED ({r.status_code})")
            return False
    except Exception as e:
        print(f"✗ API /discover Endpoint: {str(e)}")
        return False

def test_services():
    """Test all imported services"""
    print("\n" + "="*70)
    print("SERVICES VERIFICATION")
    print("="*70)
    
    services = [
        ("Master Decision Engine", "backend.services.master_decision_engine", "master_decision_engine"),
        ("User Profile Extractor", "backend.services.user_profile_extractor", "user_profile_extractor"),
        ("Eligibility Checker", "backend.services.eligibility_checker", "eligibility_checker"),
        ("Chance Estimator", "backend.services.chance_estimator", "chance_estimator"),
        ("Search Engine", "backend.services.search_engine", "search_engine"),
        ("Deduplicator", "backend.services.deduplicator", "deduplicator"),
        ("Gemini Service", "backend.services.gemini_service", "gemini_service"),
        ("Jina Search", "backend.services.jina_search", "jina_search"),
        ("Dataset Loader", "backend.services.dataset_loader", "dataset_loader"),
    ]
    
    all_ok = True
    for name, module_path, obj_name in services:
        try:
            module = __import__(module_path, fromlist=[obj_name])
            obj = getattr(module, obj_name)
            print(f"✓ {name}: LOADED")
        except Exception as e:
            print(f"✗ {name}: FAILED - {str(e)}")
            all_ok = False
    
    return all_ok

def main():
    """Run all verifications"""
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "OPPORTUNITYOS AI - APP VERIFICATION" + " "*19 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {
        "Backend": test_backend(),
        "Frontend": test_frontend_build(),
        "API Endpoint": test_api_endpoint(),
        "Services": test_services(),
    }
    
    print("\n" + "="*70)
    print("FINAL RESULTS")
    print("="*70)
    
    for component, status in results.items():
        icon = "✓" if status else "✗"
        status_text = "PASS" if status else "FAIL"
        print(f"{icon} {component}: {status_text}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("✓ APPLICATION STATUS: PRODUCTION READY")
        print("  - Backend operational")
        print("  - Frontend built")
        print("  - API responding")
        print("  - All services loaded")
        print("\n  You can now:")
        print("  1. Start backend: python -m uvicorn backend.main:app --no-reload")
        print("  2. Open frontend: http://localhost:5173")
        print("  3. Query API: http://127.0.0.1:8000/docs")
    else:
        print("✗ APPLICATION STATUS: NEEDS FIXES")
        print(f"  Failed components: {[k for k,v in results.items() if not v]}")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
