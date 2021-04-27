# ---
# From https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92

import streamlit.ReportThread as ReportThread
from streamlit.server.Server import Server


class SessionState(object):
    def __init__(self, **kwargs):
        """A new SessionState object.
        
        Parameters
        ----------
        **kwargs : any
            Default values for the session state.
            
        Example
        -------
        >>> session_state = SessionState(user_name='', favorite_color='black')
        >>> session_state.user_name = 'Mary'
        ''
        >>> session_state.favorite_color
        'black'

        """
        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    """Gets a SessionState object for the current session.
    Creates a new object if necessary.
    
    Parameters
    ----------
    **kwargs : any
        Default values you want to add to the session state, if we're creating a
        new one.
        
    Example
    -------
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    ''
    >>> session_state.user_name = 'Mary'
    >>> session_state.favorite_color
    'black'
    
    Since you set user_name above, next time your script runs this will be the
    result:
    
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    'Mary'
    
    """
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_infos.values()

    for session_info in session_infos:
        if session_info.session._main_dg == ctx.main_dg:
            session = session_info.session

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    # Got the session object! Now let's attach some state into it.

    if not getattr(session, '_custom_session_state', None):
        session._custom_session_state = SessionState(**kwargs)

    return session._custom_session_state

# ---
# From https://discuss.streamlit.io/t/preserving-state-across-sidebar-pages/107

import streamlit as st
# Normally you'd import the file above here.
# import SessionState

st.sidebar.title("Pages")
radio = st.sidebar.radio(label="", options=["Set A", "Set B", "Add them"])

# Normally you'd do this:
#session_state = SessionState.get(a=0, b=0)
# ...but since we're not importing SessionState, we'll just do:
session_state = get(a=0, b=0)  # Pick some initial values.

if radio == "Set A":
    session_state.a = float(st.text_input(label="What is a?", value=session_state.a))
    st.write(f"You set a to {session_state.a}")
elif radio == "Set B":
    session_state.b = float(st.text_input(label="What is b?", value=session_state.b))
    st.write(f"You set b to {session_state.b}")
elif radio == "Add them":
    st.write(f"a={session_state.a} and b={session_state.b}")
    button = st.button("Add a and b")
    if button:
        st.write(f"a+b={session_state.a+session_state.b}")