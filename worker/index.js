/**
 * Serve video files from R2 at /videos/<key>.
 * Static HTML under videos/ is served from Workers Assets; .mov files come from R2.
 */

const VIDEO_TYPES = {
  mov: "video/quicktime",
  mp4: "video/mp4",
  webm: "video/webm",
};

function isVideoPath(pathname) {
  const ext = pathname.split(".").pop()?.toLowerCase();
  return ext && ext in VIDEO_TYPES;
}

async function serveVideo(request, env, key) {
  if (!env.VIDEOS) {
    return new Response(
      "Video storage not configured. Bind R2 bucket VIDEOS in wrangler.jsonc.",
      { status: 503, headers: { "content-type": "text/plain" } },
    );
  }

  const range = request.headers.get("range");
  const object = await env.VIDEOS.get(key, range ? { range: request.headers } : {});

  if (object === null) {
    return new Response("Video not found", {
      status: 404,
      headers: { "content-type": "text/plain" },
    });
  }

  const headers = new Headers();
  object.writeHttpMetadata(headers);
  headers.set("etag", object.httpEtag);
  headers.set("cache-control", "public, max-age=31536000, immutable");
  headers.set("accept-ranges", "bytes");

  const ext = key.split(".").pop().toLowerCase();
  headers.set("content-type", VIDEO_TYPES[ext]);

  const status = range && object.range ? 206 : 200;
  if (object.range) {
    headers.set(
      "content-range",
      `bytes ${object.range.offset}-${object.range.offset + object.range.length - 1}/${object.size}`,
    );
  }

  return new Response(object.body, { status, headers });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { pathname } = url;

    if (pathname.startsWith("/videos/") && isVideoPath(pathname)) {
      const key = decodeURIComponent(pathname.slice("/videos/".length));
      return serveVideo(request, env, key);
    }

    return env.ASSETS.fetch(request);
  },
};
