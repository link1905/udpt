import { NavLink, useParams } from "react-router-dom";
import {
  ActionIcon,
  Avatar,
  Badge,
  Box,
  Button,
  Divider,
  Group,
  Image,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconThumbUp, IconThumbDown } from "@tabler/icons-react";
import demoImage from "../../assets/demo-image.png";
import demoAvatarImage from "../../assets/avata.jpeg";

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
  console.log(id);
  return (
    <Box>
      <Group position="apart">
        <Box>
          <Title fw={400}>Question title here</Title>
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
                  Ben Larson
                </Group>
                <Box>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam, quis nostrud exercitation ullamco
                  laboris nisi ut aliquip ex ea commodo consequat. Duis aute
                  irure dolor in reprehenderit in voluptate velit esse cillum
                  dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                  cupidatat non proident, sunt in culpa qui officia deserunt
                  mollit anim id est laborum.
                </Box>
                <Group>
                  <Image
                    maw={240}
                    mx="auto"
                    radius="md"
                    src={demoImage}
                    alt="Random image"
                  />
                  <Image
                    maw={240}
                    mx="auto"
                    radius="md"
                    src={demoImage}
                    alt="Random image"
                  />
                </Group>
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
