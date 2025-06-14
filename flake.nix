{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { system = "${system}"; };
    in
    {
      devShells.${system} = {
        default = pkgs.mkShell {
          venvDir = ".venv";
          postShellHook = ''
            set -a
            source .env.dev
            set +a
          '';
          packages =
            with pkgs;
            [
              ruff
              uv
              basedpyright
              python311
            ]
            ++ (with pkgs.python311Packages; [
              venvShellHook
              # python-lsp-server
              # python-lsp-ruff
              # black
            ]);
        };
      };
    };
}

