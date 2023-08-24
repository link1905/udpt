import React from "react";
import { Notification } from "@mantine/core";
import { IconCheck, IconX } from "@tabler/icons-react";
type AlertType = {
  color: string;
  message: string;
  title: string;
};

const CustomAlert = (props: AlertType) => {
  return (
    <Notification className="mb-3"
      icon={<IconCheck size="1.1rem" />}
      color={props.color}
      title={props.title}
    >
      {props.message}
    </Notification>
  );
};

export default CustomAlert;
