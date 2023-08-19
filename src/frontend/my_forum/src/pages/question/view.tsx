import { NavLink, useParams } from "react-router-dom";
import {
  ActionIcon,
  Avatar,
  Badge,
  Box,
  Button,
  Divider,
  Group,
  LoadingOverlay,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconThumbUp, IconThumbDown } from "@tabler/icons-react";
import demoAvatarImage from "../../assets/avata.jpeg";
import { useQuery } from "@tanstack/react-query";
import {
  getThreadQueryKey,
  requestGetThread,
} from "../../services/forum/get-thread.ts";

const tags = [
  "Tag azaaa",
  "Tag bzaaa",
  "Tag czaaa",
  "Tag dzaaa",
  "Tag ezaaa",
  "Tag fzaaa",
];

const items = [1, 2];

export function ViewQuestionPage() {
  const { id } = useParams<"id">();
  const { data, isLoading } = useQuery(
    getThreadQueryKey(id || ""),
    () => requestGetThread(id || ""),
    {
      enabled: !!id,
    },
  );
  console.log(data);
  return (
    <Box>
      <LoadingOverlay visible={isLoading} />
      <Group position="apart">
        <Box>
          <Title fw={400}>{data?.fields?.title}</Title>
          <Text fz="xs">Asked 4 years, 5 months ago</Text>
        </Box>
        <Box>
          <NavLink to="/question/create">
            <Button>Ask question</Button>
          </NavLink>
        </Box>
      </Group>
      {items.map((item) => (
        <Paper withBorder p="xl" key={item} mb="xl">
          <Group align="start">
            <Box>
              <Stack align="center">
                <ActionIcon
                  color="blue"
                  size="lg"
                  radius="xl"
                  variant="outline"
                >
                  <IconThumbUp size="1.625rem" />
                </ActionIcon>
                <Text fz="lg" fw={600}>
                  99
                </Text>
                <ActionIcon size="lg" radius="xl" variant="outline">
                  <IconThumbDown size="1.625rem" />
                </ActionIcon>
              </Stack>
            </Box>
            <Box sx={{ flex: 1 }}>
              <Stack align="start">
                <Group>
                  <Avatar src={demoAvatarImage} color="blue" radius="sm" />
                  {data?.fields?.creator_name || data?.fields?.creator_email}
                </Group>
                <Box>
                  {data?.fields?.content && (
                    <div
                      dangerouslySetInnerHTML={{
                        __html: data.fields.content,
                      }}
                    />
                  )}
                </Box>
                <Group spacing="sm">
                  {tags.map((tag) => (
                    <Badge key={tag}>{tag}</Badge>
                  ))}
                </Group>
              </Stack>
              <Divider my="md" />
              <Stack>
                <Group>
                  <Avatar
                    src={demoAvatarImage}
                    color="blue"
                    radius="sm"
                    size="sm"
                  />
                  <Text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                    do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Maecenas pharetra convallis posuere morbi leo urna
                    molestie at. Et egestas quis ipsum suspendisse ultrices
                    gravida dictum
                  </Text>
                </Group>
                <Group>
                  <Avatar
                    src={demoAvatarImage}
                    color="blue"
                    radius="sm"
                    size="sm"
                  />
                  <Text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                    do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Maecenas pharetra convallis posuere morbi leo urna
                    molestie at. Et egestas quis ipsum suspendisse ultrices
                    gravida dictum
                  </Text>
                </Group>
              </Stack>
            </Box>
          </Group>
        </Paper>
      ))}
    </Box>
  );
}
