import os
import re

def scan_gitignore():
    print("\n🔍 Scanning .gitignore...")
    if not os.path.exists('.gitignore'):
        print("  ❌ ERROR: .gitignore file is missing.")
        return

    with open('.gitignore', 'r') as f:
        content = f.read()
        lines = content.splitlines()
    
    if '.env' in lines or '*.env' in lines:
        print("  ✅ SUCCESS: .env is properly ignored.")
    else:
        print("  ❌ ERROR: .env is NOT in .gitignore. You risk leaking secrets!")

    if '.env.example' in lines:
        print("  ❌ ERROR: .env.example is ignored. It SHOULD be committed to version control.")
    else:
        print("  ✅ SUCCESS: .env.example is not ignored.")

def parse_env_file(filepath):
    keys = {}
    if not os.path.exists(filepath):
        return keys
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                keys[key.strip()] = val.strip()
    return keys

def scan_environments():
    print("\n🔍 Scanning .env and .env.example...")
    
    has_env = os.path.exists('.env')
    has_example = os.path.exists('.env.example')
    
    if not has_env:
        print("  ⚠️ WARNING: .env file missing. (Ignore if this is a fresh clone).")
    if not has_example:
        print("  ❌ ERROR: .env.example file missing. You should provide a template.")
        
    env_keys = parse_env_file('.env')
    example_keys = parse_env_file('.env.example')

    # Check .env for missing values
    if has_env:
        empty_vals = [k for k, v in env_keys.items() if not v]
        if empty_vals:
            print(f"  ⚠️ WARNING: .env has empty values for: {', '.join(empty_vals)}")
        else:
            print("  ✅ SUCCESS: .env is populated correctly.")

    # Check .env.example for leaked secrets
    if has_example:
        suspicious_vals = [k for k, v in example_keys.items() if len(v) > 5 and 'your' not in v.lower()]
        if suspicious_vals:
            print(f"  ❌ ERROR: .env.example might contain actual secrets for: {', '.join(suspicious_vals)}")
        else:
            print("  ✅ SUCCESS: .env.example appears to be safely scrubbed.")

    # Compare keys between the two
    if has_env and has_example:
        env_set = set(env_keys.keys())
        example_set = set(example_keys.keys())
        
        missing_in_example = env_set - example_set
        missing_in_env = example_set - env_set
        
        if missing_in_example:
            print(f"  ❌ ERROR: Keys in .env but missing in .env.example: {', '.join(missing_in_example)}")
        if missing_in_env:
            print(f"  ⚠️ WARNING: Keys in .env.example but missing in .env: {', '.join(missing_in_env)}")

def scan_readme():
    print("\n🔍 Scanning README.md...")
    readme_names = ['README.md', 'readme.md', 'README.txt']
    readme_file = next((f for f in readme_names if os.path.exists(f)), None)

    if not readme_file:
        print("  ❌ ERROR: No README file found.")
        return

    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    if '.env' in content or 'environment variable' in content:
        print("  ✅ SUCCESS: README mentions environment variables / .env setup.")
    else:
        print("  ❌ ERROR: README does not explain how to set up the .env file. Add instructions!")

if __name__ == "__main__":
    print("========================================")
    print("      .ENV REPOSITORY SCANNER")
    print("========================================")
    scan_gitignore()
    scan_environments()
    scan_readme()
    print("\n========================================")
    print("             SCAN COMPLETE")
    print("========================================\n")
