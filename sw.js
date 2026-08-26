const CACHE_NAME="ouvidoria-rhp-v41";
const STATIC_ASSETS=[
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install",event=>{
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache=>cache.addAll(STATIC_ASSETS)).then(()=>self.skipWaiting())
  );
});

self.addEventListener("activate",event=>{
  event.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener("fetch",event=>{
  const req=event.request;
  if(req.method!=="GET")return;

  const url=new URL(req.url);

  // Never cache Supabase/API/auth/storage traffic or other cross-origin requests.
  if(url.origin!==self.location.origin)return;

  // Navigation: serve network first; shell fallback only if offline.
  if(req.mode==="navigate"){
    event.respondWith(
      fetch(req).catch(()=>caches.match("./index.html"))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then(cached=>cached||fetch(req))
  );
});


self.addEventListener("message",event=>{
  if(event.data?.type==="SKIP_WAITING")self.skipWaiting();
});

self.addEventListener("push",event=>{
  let data={title:"OUVIDORIA RHP",body:"NOVA NOTIFICAÇÃO RECEBIDA.",url:"./index.html"};
  try{data={...data,...event.data.json()};}catch(e){}
  event.waitUntil(self.registration.showNotification(data.title,{
    body:data.body,
    icon:"./icons/icon-192.png",
    badge:"./icons/icon-192.png",
    data:{url:data.url||"./index.html",protocol_id:data.protocol_id||null},
    tag:data.protocol_id?`protocolo-${data.protocol_id}`:"ouvidoria",
    renotify:true
  }));
});

self.addEventListener("notificationclick",event=>{
  event.notification.close();
  const target=new URL(event.notification.data?.url||"./index.html",self.location.origin).href;
  event.waitUntil((async()=>{
    const clientsList=await clients.matchAll({type:"window",includeUncontrolled:true});
    for(const client of clientsList){
      if("focus" in client){await client.focus();if("navigate" in client)await client.navigate(target);return;}
    }
    if(clients.openWindow)return clients.openWindow(target);
  })());
});
