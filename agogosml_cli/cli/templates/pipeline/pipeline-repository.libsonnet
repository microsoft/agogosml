{
    Repository(type = 'GitHub', url = 'https://github.com/Microsoft/agogosml.git', owner = 'Microsoft', repo = 'agogosml'): {
        "properties": {},
        "id": std.join('/', [owner, repo]),
        "type": type,
        "name": std.join('/', [owner, repo]),
        "url": url,
        "defaultBranch": "master",
        "clean": "false",
        "checkoutSubmodules": false
    }
}