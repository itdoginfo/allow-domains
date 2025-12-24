{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.tldextract
    sing-box
  ];

  shellHook = ''
    echo "Environment ready!"
    echo "Python version: $(python --version)"
    echo "sing-box version: $(sing-box version 2>/dev/null || echo 'not available')"
  '';
}
