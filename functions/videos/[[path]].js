/**
 * Serve video files from R2 at /videos/<key>.
 * HTML pages under videos/ (e.g. /videos/deming/01/) are static assets from Pages.
 * Only media requests (.mov, .mp4, .webm) reach this function.
 */

const VIDEO_TYPES = {
  mov: "video/quicktime",
  mp4: "video/mp4",
  webm: "video/webm",
};

function isVideoKey(key) {
  const ext = key.split(".").pop()?.toLowerCase();
  return ext && ext in VIDEO_TYPES;
}

export async function onRequest({ request, env, params }) {
  const key = decodeURIComponent(params.path || "");

  if (!key || !isVideoKey(key)) {
    return new Response("Not found", { status: 404 });
  }

  if (!env.VIDEOS) {
    return new Response(
      "Video storage not configured. Bind R2 bucket VIDEOS in Pages settings.",
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
