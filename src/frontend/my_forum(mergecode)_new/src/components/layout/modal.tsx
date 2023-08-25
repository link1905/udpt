import { Modal, Text } from "@mantine/core";

export function ThreadModal({ thread, onClose }) {
  return (
    <Modal opened onClose={onClose} title={thread.title}>
      <Text>{thread.content}</Text>
    </Modal>
  );
}
