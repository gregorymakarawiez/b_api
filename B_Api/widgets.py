from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class ScriptWidget(forms.MultiWidget):
    def __init__(self,attrs=None,*args,**kwargs):
        widgets=[
            forms.TextInput(attrs={'placeholder':'language'}),
            forms.TextInput(attrs={'placeholder':'code'})
        ]

        super(ScriptWidget, self).__init__(widgets=widgets,*args,**kwargs)

    def decompress(self, value):
        if value:
            return value.split(" ")
        return [None, None]

    def format_output(self, rendered_widgets):
         html_output=''.join(rendered_widgets)
         return html_output



class MyAceWidget(forms.Widget):

    def render(self, name, value, attrs=None):    
        flat_attrs = flatatt(attrs)

        print("<<<<<<<<<<<")
        print(name)
        print(value)
        print(">>>>>>>>>>>>>>")

        html='''
        <textarea name="%(name)s" style="display:none;"> %(value)s </textarea>
        <div id="%(name)s"> %(value)s </div>
    

        <script>
            // get handles to DOM widgets
            var ace_%(name)s = ace.edit('%(name)s');                // ace editor
            var textarea_%(name)s = $('textarea[name="%(name)s"]'); // hidden textarea to save editor content

            // initialize editor
            ace_%(name)s.setTheme("ace/theme/monokai");            // choose look and feel (see ace doc for other choices)
            ace_%(name)s.getSession().setMode("ace/mode/python");  // select python language
            ace_%(name)s.setOptions({
            maxLines: 15                                           // editor height (longer codes will make a scrolling bar appear on the right)
            });
            ace_%(name)s.getSession().setValue(textarea_%(name)s.val()); // on DOM loading, copy hidden textarea content into ace editor
            ace_%(name)s.getSession().on("change", function () {      
                textarea_%(name)s.val(ace_%(name)s.getSession().getValue()); // whenever ace editor content change, copy change back into hidden textarea
            });
        </script>
''' % {'name': name,'value':value}

        return mark_safe(html)



 
    def value_from_datadict(self, data, files, name):
        print(data.get(name, name))
        return data.get(name, name)



class MyQuillWidget(forms.Widget):
# some documentation on how to embed Quill in a web site 
#https://quilljs.com/docs/quickstart/

    def render(self, name, value, attrs=None):    
        flat_attrs = flatatt(attrs)

        print("<<<<<<<<<<<")
        print(name)
        print(value)
        print(">>>>>>>>>>>>>>")

        html_old='''
        <!--<textarea name="%(name)s" style="display:none;"> %(value)s </textarea>-->
        <textarea name="%(name)s" > %(value)s </textarea>

        <div id="%(name)s_editor" class="quill_editor"> 
            <div id="%(name)s_toolbar"></div>
            <div id="%(name)s_content">
	        <!--%(value)s-->
            </div>
        </div>
    

        <script>
            // get handles to DOM widgets
            var quill_%(name)s = new Quill('#%(name)s_content',{ // ace editor
                modules:{
                    toolbar:[
                        //[{header:[1,2,false]}],
                        //['bold','italic','underline']
                        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                        ['blockquote', 'code-block'],
                        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
                        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
                        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
                        [{ 'direction': 'rtl' }],                         // text direction
                        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                        [{ 'font': [] }],
                        [{ 'align': [] }],
                        ['clean']                                         // remove formatting button
                    ],
                },
                placeholder: 'compose an epic...',
                theme: 'snow'
            });
                




            var textarea_%(name)s = $('textarea[name="%(name)s"]'); // hidden textarea to save editor content
            var insert_text=textarea_%(name)s.val();
            if (insert_text==' None '){
               insert_text='';
            }
            quill_%(name)s.insertText(0,insert_text); // on DOM loading, copy hidden textarea content into quill editor
            quill_%(name)s.on("text-change", function () {      
                textarea_%(name)s.val(quill_%(name)s.getText()); // whenever quill editor content change, copy change back into hidden textarea
            });
        </script>
        ''' % {'name': name,'value':value}


        html='''
        <textarea name="%(name)s" style="display:none;"> %(value)s </textarea>
        
        <div id="%(name)s_editor" class="quill_editor"> 
            <div id="%(name)s_toolbar"></div>
            <div id="%(name)s_content">
	        <!--%(value)s-->
            </div>
        </div>
    

        <script>
            // instantiate quill editor
            var quill_%(name)s = new Quill('#%(name)s_content',{ // ace editor
                modules:{
                    toolbar:[
                        //[{header:[1,2,false]}],
                        //['bold','italic','underline']
                        [{ 'font': [] }],
                        [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
                        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
                        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
                        [{ 'list': 'ordered'},{ 'list': 'bullet'}],
                        [{ 'align': [] }]
                    ],
                },
                placeholder: 'compose an epic...',
                theme: 'snow'
            });
                
            // create handle to DOM hidden textarea 
            var textarea_%(name)s = $('textarea[name="%(name)s"]'); // hidden textarea to save editor content

            // on page loading, get db saved content that django has restored into DOM hidden textarea 
            var insert_text=textarea_%(name)s.val();
            if (insert_text==' None '){
               insert_text='';
            }
    
            try{
                var insert_json=JSON.parse(insert_text);
            }
            catch(e){
                 console.error("Parsing error:", e);
            }
            quill_%(name)s.setContents(insert_json); // on DOM loading, copy hidden textarea content into quill editor
            quill_%(name)s.on("text-change", function () { 
                var save_json=quill_%(name)s.getContents() ;
                var save_txt=JSON.stringify(save_json);  
                textarea_%(name)s.val(save_txt); // whenever quill editor content change, copy change back into hidden textarea
            });
        </script>
        ''' % {'name': name,'value':value}

        return mark_safe(html)



 
    def value_from_datadict(self, data, files, name):
        print(data.get(name, name))
        return data.get(name, name)

