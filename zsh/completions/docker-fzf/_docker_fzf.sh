# fzf-based zsh completion for docker
_docker_fzf_zsh() {
  local words=(${=BUFFER})
  local cmd
  for ((i=2; i<${#words}; i++)); do
    [[ ${words[i]} != -* ]] && cmd=${words[i]} && break
  done

  _fzf_choose() {
    local type=$1
    if [[ $type == container ]]; then
      docker ps -a --format $'{{.Names}}\t{{.Image}}\t{{.Status}}' \
        | fzf --height=40% --reverse --with-nth=1 \
        | cut -f1
    else
      docker images --format $'{{.Repository}}:{{.Tag}}\t{{.ID}}' \
        | fzf --height=40% --reverse --with-nth=1 \
        | cut -f1
    fi
  }

  case "$cmd" in
    logs|exec|inspect|attach|start|stop|rm|restart|kill|cp)
      compadd -- $(_fzf_choose container)
      ;;
    run|rmi|pull|push|tag)
      compadd -- $(_fzf_choose image)
      ;;
    *)
      compadd -- $(_fzf_choose container)
      ;;
  esac
}

