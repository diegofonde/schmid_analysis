import streamlit as st
import streamlit.components.v1 as components

st.title("Interactive Tableau Dashboard 📊")

st.markdown("""
Welcome to the data visualization hub! This page features an interactive Tableau dashboard hosted on Tableau Public, 
designed to bring our Qualtrics survey responses to life. 

**Dashboards you can explore here:**
* 👤 **Student Profile:** Understand key demographics of students who responded to the survey.
* 📈 **Resource Analysis:** Deep dive analysis into resource use and student resource preference.
* 🤝 **Schmid Environment & Sense of Belonging:** Discover how Schmid students feel about the college based on major.

*Click on the filters on the side to filter dynamically, and explore the insights at your own pace.*
""")

tableau_url = "https://public.tableau.com/app/profile/diego.gabriel.fondevilla/viz/Schmid_Survey/StudentProfile?publish=yes"
tableau_embedded_code = """
<div class='tableauPlaceholder' id='viz1783002768655' style='position: relative'>
<noscript>
<a href='#'>
<img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;Schmid_Survey&#47;StudentProfile&#47;1_rss.png' style='border: none' /></a></noscript>
<object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
<param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Schmid_Survey&#47;StudentProfile' />
<param name='tabs' value='yes' /><param name='toolbar' value='yes' />
<param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Sc&#47;Schmid_Survey&#47;StudentProfile&#47;1.png' /> 
<param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' />
<param name='display_overlay' value='yes' /><param name='display_count' value='yes' />
<param name='language' value='en-US' /><param name='filter' value='publish=yes' />
</object></div>                
<script type='text/javascript'>                    
var divElement = document.getElementById('viz1783002768655');                    
var vizElement = divElement.getElementsByTagName('object')[0];                    
if ( divElement.offsetWidth > 800 ) { 
vizElement.style.minWidth='1366px';
vizElement.style.maxWidth='100%';
vizElement.style.minHeight='818px';
vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';
} 
else if ( divElement.offsetWidth > 500 ) 
{ vizElement.style.minWidth='1366px';
vizElement.style.maxWidth='100%';vizElement.style.minHeight='818px';
vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';
} 
else { 
vizElement.style.width='100%';
vizElement.style.minHeight='2050px';
vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';
}                     
var scriptElement = document.createElement('script');                    
scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
vizElement.parentNode.insertBefore(scriptElement, vizElement);                
</script>
"""

components.html(tableau_embedded_code, height = 750, width = 1500,scrolling = True)
