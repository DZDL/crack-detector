mkdir -p ~/.streamlit

bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml'

bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml'

gdown --id 12-iXK656aGUIWCtN9gb0Ko7qotyn9ZcI -O ./checkpoints/deepcrack/latest_net_G.pth