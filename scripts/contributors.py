import matplotlib.pyplot as plt
import streamlit as st

from scripts.variables import var
from scripts.helperFunctions import save_fig
from io import BytesIO

def user_contributions(data):
    print("=========================")
    print("Contribution of each user")
    print("=========================")
    for i,contributor in enumerate(data,start=1):
        print(f"{i}.", contributor['login'],':', contributor['contributions'])

def lowest_contributors(data,log,n=var.numof_lowest_contributions):
    '''
    finding the lowest contributors with contributions<n.
    by default n=100
    '''

    log("==================================================")
    log(f"Finding lowest {n} contributors in '{var.repo}'")
    log("==================================================")
    #low=sorted(data, key=lambda x:x['contributions'],reverse=False)
    
    var.lowest_contribution=[user for user in data if user['contributions']<n]

    log(f"Users with ≤{n} contributions: {len(var.lowest_contribution)}")
    x,y=[],[]
    for i,user in enumerate(var.lowest_contribution,start=1):
        if user['type'] == 'User':
            log(f"{i}. {user['login']} - {user['contributions']}")
            x.append(user['login'])
            y.append(user['contributions'])
        
        elif user['type'] == 'bot' or 'Bot':
            #print('Bot detected! Ignoring!')
            pass

    return var.lowest_contribution

def lowest_contributors_VIZ(data, n=var.numof_lowest_contributions, use_streamlit=False, st_output_area=None):
    """
    Generates a plot of users with contributions < n.
    Can be rendered in Streamlit or standalone.

    Args:
        data (list): GitHub user data.
        n (int): Contribution threshold.
        use_streamlit (bool): Enable Streamlit output.
        st_output_area: Optional Streamlit container (e.g., st.container()).
    """
    lowest = [user for user in data if user.get('contributions', 0) < n]

    x, y = [], []
    for user in lowest:
        if user.get('type') == 'User':
            x.append(user.get('login'))
            y.append(user.get('contributions'))
        elif user.get('type') in ['bot', 'Bot']:
            continue  # Skip bots

    if not x:
        msg = f"No users found with less than {n} contributions."
        if use_streamlit and st_output_area:
            st_output_area.warning(msg)
        elif use_streamlit:
            import streamlit as st
            st.warning(msg)
        else:
            print(msg)
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, marker='o', linestyle='-', color='tab:blue')

    for xi, yi in zip(x, y):
        ax.text(xi, yi + 0.5, str(yi), ha='center', va='bottom', fontsize=9)

    ax.set_title(f"Users with < {n} Contributions", fontsize=16)
    ax.set_xlabel("Username", fontsize=12)
    ax.set_ylabel("# of Contributions", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    if use_streamlit:
        '''
        buf = BytesIO()
        fig.savefig(buf, format="png")
        if st_output_area:
            st_output_area.image(buf.getvalue(), caption="Least Contributors", use_column_width=True)
        else:
            st.image(buf.getvalue(), caption="Least Contributors", use_column_width=True)
        '''
        import streamlit as st
        if st_output_area:
            with st_output_area:
                st.pyplot(fig)
        else:
            st.pyplot(fig)
    else:
        try:
            save_fig(name="Least contributors.png")
            print("✅ Saved: 'Least contributors.png'")
        except Exception as e:
            print(f"❌ Failed to save the image: {e}")
        plt.show()

def top_contributors(data,log,n=var.numof_top_contributors):
    '''
    Using the response, printing the most contributors, 5 by default
    '''
    log("=================================================")
    log(f"Finding top {n} contributors in '{var.repo}'")
    log("=================================================")
    var.top_contributors = sorted(data, key=lambda x: x['contributions'], reverse=True)

    for i, user in enumerate(var.top_contributors[:n], start=1):
        log(f"{i}. {user['login']} - {user['contributions']} contributions")

def top_contributors_VIZ(data, n=var.numof_top_contributors, use_streamlit=False, st_output_area=None):
    """
    Visualizes the top `n` contributors using matplotlib.
    If `use_streamlit` is True, displays the plot in Streamlit.
    Otherwise, saves the figure locally.

    Parameters:
    - data: List of contributor dicts.
    - n: Number of top contributors to show.
    - use_streamlit: Whether to display in Streamlit.
    - st_output_area: Optional Streamlit container to show the plot in.
    """

    # Sort and select top contributors
    top = sorted(data, key=lambda x: x['contributions'], reverse=True)[:n]
    names = [user['login'] for user in top]
    contribs = [user['contributions'] for user in top]

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, contribs, color='skyblue')

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(height),
            ha='center', va='bottom'
        )

    ax.set_title(f"Top {n} Contributors")
    ax.set_xlabel("Username")
    ax.set_ylabel("Contributions")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if use_streamlit:
        import streamlit as st
        if st_output_area:
            with st_output_area:
                st.pyplot(fig)
        else:
            st.pyplot(fig)
    else:
        try:
            save_fig(name="Top 10 contributors.png")
            print(f"✅ Saved: 'Top {n} contributors.png'")
        except Exception as e:
            print(f"❌ Failed to save the highest contributors image. Error:\n{e}")
    
    plt.close(fig)  # Avoid memory issues in Streamlit