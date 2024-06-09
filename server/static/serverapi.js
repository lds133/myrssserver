



class RDServer
{

    constructor(controlurl)
    {   
        this.ctrlurl = controlurl;
    }




    API(filename, resultfunc = null,resultfuncparam = null)
    {
        this.#APIGet(filename, resultfunc, resultfuncparam);
    }
	
	
    #APIGet(filename, resultfunc, resultfuncparam)
    {
        const url = this.ctrlurl;

        $.ajax({
            url: url+filename,
            type: 'get',
            beforeSend: function () { console.log("API","BEFORE"); },
            success: function (result) 
            {   console.log("API","OK",result);
                if (resultfunc != null)
                    resultfunc(result,resultfuncparam);
            },
            error: function (req, status, error) 
            {   console.log("API","ERROR",req, status, error);
                if (resultfunc != null)
                    resultfunc(null,resultfuncparam);
            }
        });

    }	
	

/*

    #APIPost(data, resultfunc, resultfuncparam)
    {
        const url = this.ctrlurl;

        $.ajax({
            url: url,
            type: 'post',
            data: data,
            dataType: 'json',
            beforeSend: function () { console.log("API","BEFORE"); },
            success: function (result) 
            {   console.log("API","OK",result);
                if (resultfunc != null)
                    resultfunc(result,resultfuncparam);
            },
            error: function (req, status, error) 
            {   console.log("API","ERROR",req, status, error);
                if (resultfunc != null)
                    resultfunc(null,resultfuncparam);
            }
        });

    }

*/

}