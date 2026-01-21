{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.matplotlib
    python3Packages.numpy
    python3Packages.networkx
    python3Packages.scipy

    p7zip
    zip
  ];
}
