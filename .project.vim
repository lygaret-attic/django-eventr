autocmd FileType python set ft=python.django " For SnipMate
autocmd FileType html set ft=html.django_template " For SnipMate
let &tags .= "," . fnamemodify("tags", ":p")
