"""
Test script to diagnose DuckDuckGo search issues
"""

print("Testing DuckDuckGo search connectivity...\n")

# Test 1: Basic internet connectivity
print("1. Testing basic internet connectivity...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://www.google.com', timeout=10)
    print("   ✓ Can reach Google")
except Exception as e:
    print(f"   ✗ Cannot reach Google: {e}")

# Test 2: DuckDuckGo website
print("\n2. Testing DuckDuckGo website...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://duckduckgo.com', timeout=10)
    print("   ✓ Can reach DuckDuckGo website")
except Exception as e:
    print(f"   ✗ Cannot reach DuckDuckGo: {e}")

# Test 3: Try ddgs library directly
print("\n3. Testing ddgs library...")
try:
    from duckduckgo_search import DDGS
    print("   ✓ ddgs library imported successfully")
    
    # Try a simple search
    print("   Attempting a simple search...")
    ddgs = DDGS(timeout=20)
    results = list(ddgs.text("test query", max_results=1))
    print(f"   ✓ Search successful! Got {len(results)} result(s)")
    
except ImportError as e:
    print(f"   ✗ ddgs library not found: {e}")
except Exception as e:
    print(f"   ✗ Search failed: {e}")

# Test 4: Try LangChain's DuckDuckGoSearchResults
print("\n4. Testing LangChain's DuckDuckGo tool...")
try:
    from langchain_community.tools import DuckDuckGoSearchResults
    search = DuckDuckGoSearchResults(num_results=2)
    print("   ✓ Tool initialized")
    
    print("   Attempting search via LangChain...")
    results = search.invoke("python programming")
    print(f"   ✓ LangChain search successful!")
    print(f"   Results preview: {results[:200]}...")
    
except Exception as e:
    print(f"   ✗ LangChain search failed: {e}")

print("\n" + "="*50)
print("Diagnostic complete!")
