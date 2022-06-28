let showing = false

function columnsController()
{
    let columnsDiv = document.getElementById("columns-div");

    if (!showing)
    {
        columnsDiv.style.display = "block";
        showing = true;
    }
    else
    {
        columnsDiv.style.display = "none";
        showing = false;
    }
}
