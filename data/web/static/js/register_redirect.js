function redirect(){
    const nextUrl = new URL(window.location.href);
    const next = nextUrl.searchParams.get('next');
    if(next){
        window.location.href = '/user/register/?next=' + encodeURIComponent(next);
    } else {
        window.location.href = '/user/register/'
    }
}