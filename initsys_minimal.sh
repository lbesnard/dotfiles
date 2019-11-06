#!/usr/bin/env bash

## script to install a functional working env on the $HOME directory
## using linuxbrew
## will install tools such as zsh, tmux, ranger, fzf ... and dotfiles
# install manually https://github.com/alexanderjeurissen/ranger_devicons

mkdir -p $HOME/usr/bin
export PATH="$HOME/usr/bin:$PATH"

# install linuxbrew
# if user has sudo privileges, linuxbrew should be installed in /home/linuxbrew
# Otherwise the install script will automatically setup brew under $HOME/.linuxbrew
if ! [ -x "$(command -v brew)" ]; then
	sh -c "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh)"
fi

# check where is installed linuxbrew
if [[ -d $HOME/.linuxbrew ]]; then
    export HOMEBREW_PREFIX=$HOME/.linuxbrew
elif [[ -d /home/linuxbrew ]]; then
    export HOMEBREW_PREFIX=/home/linuxbrew/.linuxbrew
fi

eval $($HOMEBREW_PREFIX/bin/brew shellenv)

export PATH="$HOMEBREW_PREFIX/bin:$PATH"
export MANPATH="$HOMEBREW_PREFIX/share/man:$MANPATH"
export INFOPATH="$HOMEBREW_PREFIX/share/info:$INFOPATH"

# install or upgrade brew packages
function brew_install_or_upgrade {
    if brew ls --versions "$1" >/dev/null; then
        HOMEBREW_NO_AUTO_UPDATE=1 brew upgrade "$1"
    else
        HOMEBREW_NO_AUTO_UPDATE=1 brew install "$1"
    fi
}

# see https://github.com/Linuxbrew/homebrew-core/issues/955#issuecomment-250151297
export HOMEBREW_ARCH=core2

# install or upgrade pacakge in $HOME directory
brew_install_or_upgrade gcc
brew_install_or_upgrade ruby
brew_install_or_upgrade fzf
brew_install_or_upgrade zsh
brew_install_or_upgrade tmux
brew_install_or_upgrade autojump
brew_install_or_upgrade vim
brew_install_or_upgrade lnav

# To install useful key bindings and fuzzy completion for fzf
$(brew --prefix)/opt/fzf/install
[[ -s $(brew --prefix)/etc/profile.d/autojump.sh ]] && . $(brew --prefix)/etc/profile.d/autojump.sh

# setup dotfiles
if [ -d $HOME/github_repo/dotfiles ];then # on local computer
    export DOTFILES_PATH=$HOME/github_repo/dotfiles && cd $DOTFILES_PATH
    git pull
elif [ -d $HOME/dotfiles >/dev/null ]; then # on any $HOME folder, the dotfiles repo should be clone to $HOME/dotfiles
    export DOTFILES_PATH=$HOME/dotfiles && cd $DOTFILES_PATH
    git pull;
else
    git clone https://github.com/lbesnard/dotfiles.git;
    export DOTFILES_PATH=$HOME/dotfiles
fi
. $DOTFILES_PATH/install

#curl -fsSL -o .gitconfig https://raw.githubusercontent.com/lbesnard/dotfiles/master/gitconfig

export SHELL=$HOMEBREW_PREFIX/bin/zsh
export PATH="$HOME/usr/bin:$PATH"

#add line to bashrc only if not exist
add_line_bashrc() {
    local line="$1"; shift
    grep -q "^${line}$" $HOME/.bashrc ||  echo $line >> $HOME/.bashrc
}

#add_line_bashrc "export HOMEBREW_PREFIX=${HOMEBREW_PREFIX}"
add_line_bashrc "export PATH=$HOMEBREW_PREFIX/bin:$PATH"
add_line_bashrc "export MANPATH=$HOMEBREW_PREFIX/share/man:$MANPATH"
add_line_bashrc "export INFOPATH=$HOMEBREW_PREFIX/share/info:$INFOPATH"
add_line_bashrc "export SHELL=$HOMEBREW_PREFIX/bin/zsh"
add_line_bashrc "$HOMEBREW_PREFIX/bin/zsh"

# update vim
if [ -d $HOME/.vim/utoload/plug.vim ];then
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
fi

vim +PlugInstall!