import { IconPhoto } from "@tabler/icons-react";
import { useRef } from "react";
import { RichTextEditor } from "@mantine/tiptap";

export function ImageUploader({
  onUploaded,
}: {
  onUploaded: (src: string) => void;
}) {
  const ref = useRef<HTMLInputElement>(null);
  return (
    <>
      <RichTextEditor.Control
        onClick={() => ref?.current?.click()}
        aria-label="Insert star emoji"
        title="Insert star emoji"
      >
        <IconPhoto stroke={1.5} size="1rem" />
      </RichTextEditor.Control>
      <input
        onChange={(e) => {
          if (e.target?.files?.length) {
            const FR = new FileReader();
            console.log(2, onUploaded);
            FR.addEventListener("load", function (evt) {
              console.log(evt?.target?.result);
              onUploaded(String(evt?.target?.result));
            });

            FR.readAsDataURL(e.target.files[0]);
          }
        }}
        type="file"
        accept="image/png, image/gif, image/jpeg"
        ref={ref}
        style={{ display: "none" }}
      />
    </>
  );
}
