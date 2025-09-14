def test_web_index_exists():
    import os
    assert os.path.exists('src/web/templates/index.html')
